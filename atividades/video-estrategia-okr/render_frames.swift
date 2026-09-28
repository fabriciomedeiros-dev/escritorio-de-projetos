import Foundation
import AppKit
import ImageIO
import CoreGraphics

let work=URL(fileURLWithPath:CommandLine.arguments[1])
let out=URL(fileURLWithPath:CommandLine.arguments[2])
let duration=177.00884353741498
let w=1280,h=720,fps=10
let weights=[30.0,47.0,38.0,78.0,125.0,72.0,40.0,45.0]
let sum=weights.reduce(0,+)
var starts=[Double](); var cursor=0.0
for v in weights { starts.append(cursor);cursor += duration*v/sum };starts.append(duration)
let slides=(1...8).map { n -> CGImage in
 let url=work.appendingPathComponent(String(format:"slide-%02d.png",n))
 guard let src=CGImageSourceCreateWithURL(url as CFURL,nil),let cg=CGImageSourceCreateImageAtIndex(src,0,nil) else { fatalError("Cannot read \(url.path)") }
 return cg
}
let chart=(0...4).map { n -> CGImage in
 let url=work.appendingPathComponent(String(format:"slide-05-step-%d.png",n))
 guard let src=CGImageSourceCreateWithURL(url as CFURL,nil),let cg=CGImageSourceCreateImageAtIndex(src,0,nil) else { fatalError("Cannot read \(url.path)") }
 return cg
}
try? FileManager.default.removeItem(at:out)
try FileManager.default.createDirectory(at:out,withIntermediateDirectories:true)
let rgb=CGColorSpaceCreateDeviceRGB()
let total=Int(duration*Double(fps))
for index in 0..<total {
 autoreleasepool {
  let t=Double(index)/Double(fps)
  var scene=0
  for i in 1..<starts.count where t>=starts[i] { scene=i }
  scene=min(scene,7)
  let local=t-starts[scene]
  let sceneLength=starts[scene+1]-starts[scene]
  var current=slides[scene]
  if scene==4 && local<5 { current=chart[min(4,Int(local/1.25))] }
  let fade=1.15
  let blending=scene<7 && local>sceneLength-fade
  let alpha=blending ? min(1,max(0,(local-(sceneLength-fade))/fade)) : 0
  guard let ctx=CGContext(data:nil,width:w,height:h,bitsPerComponent:8,bytesPerRow:0,space:rgb,bitmapInfo:CGImageAlphaInfo.noneSkipLast.rawValue) else { fatalError("Cannot create context") }
  ctx.setFillColor(CGColor(red:11/255,green:23/255,blue:48/255,alpha:1));ctx.fill(CGRect(x:0,y:0,width:w,height:h))
  let zoom=1.0+0.018*min(1,max(0,local/max(1,sceneLength)))
  let dst=CGRect(x:-(Double(w)*(zoom-1)/2),y:-(Double(h)*(zoom-1)/2),width:Double(w)*zoom,height:Double(h)*zoom)
  ctx.draw(current,in:dst)
  if blending { ctx.setAlpha(alpha);ctx.draw(slides[min(scene+1,7)],in:dst);ctx.setAlpha(1) }
  guard let cg=ctx.makeImage() else { fatalError("Cannot create image") }
  let path=out.appendingPathComponent(String(format:"frame-%05d.jpg",index))
  guard let dest=CGImageDestinationCreateWithURL(path as CFURL,"public.jpeg" as CFString,1,nil) else { fatalError("Cannot create JPEG") }
  CGImageDestinationAddImage(dest,cg,[kCGImageDestinationLossyCompressionQuality:0.78] as CFDictionary)
  if !CGImageDestinationFinalize(dest) { fatalError("Cannot finalize JPEG") }
 }
 if index % 100 == 0 { print("Quadros: \(index)/\(total)") }
}
print("Renderizados \(total) quadros")
